# チュートリアル

## FastAPI Webアプリケーションでのロギング

このチュートリアルでは、`provide.foundation` をシンプルな **FastAPI** ウェブアプリケーションに統合する方法を順を追って説明します。アプリケーションのセットアップから、リクエストのロギング、ビジネスロジックの計測まで、多くの重要な概念をカバーします。

このチュートリアルを終える頃には、あらゆるウェブアプリケーションで美しく、構造化された、意味のあるログを生成するための確かな基礎を身につけていることでしょう。

### 前提条件

開始する前に、必要なライブラリがインストールされていることを確認してください。

```bash
pip install provide-foundation fastapi "uvicorn[standard]"
```

### ステップ1：基本的なFastAPIアプリケーションのセットアップ

まず、`main.py` という名前のファイルを作成し、基本的なFastAPIアプリケーションをセットアップします。

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

### ステップ2：起動時のロガーの初期化

`provide.foundation` を設定するのに最適な場所は、アプリケーションの起動時です。FastAPIの `lifespan` イベントを使用して、サーバーが起動するときに一度だけ `setup_telemetry` を呼び出すようにします。

このステップでは、`http` と `database` のセマンティックレイヤーも有効にします。

```python
# main.py
import contextlib
from fastapi import FastAPI

from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig

# lifespanイベント内でロガーを設定
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    print("アプリケーションの起動時にテレメトリを設定しています...")
    config = TelemetryConfig(
        service_name="my-fastapi-app",
        logging=LoggingConfig(
            default_level="INFO",
            # HTTPとデータベースのセマンティックレイヤーを有効にする
            enabled_semantic_layers=["http", "database"],
        ),
    )
    setup_telemetry(config)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

### ステップ3：ミドルウェアによるリクエストのロギング

すべての受信リクエストとそのレスポンスを自動的にログに記録することは、非常に強力なパターンです。FastAPIミドルウェアを使用してこれを実現できます。

```python
# main.py (前のコードに追加)
import time
from fastapi import Request
from provide.foundation import logger

# ... (FastAPIのセットアップとlifespanは上記と同じ)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start_time) * 1000

    logger.info(
        "HTTP request handled",
        **{
            "http.method": request.method,
            "http.url": str(request.url),
            "http.status_code": response.status_code,
            "http.response_time_ms": round(duration_ms, 2),
            "client.address": request.client.host,
        },
    )

    return response

# ... (ルートとエンドポイントは下記)
```

### ステップ4：エンドポイントでのロギング

次に、ユーザーを作成するための `/users` エンドポイントを追加します。このエンドポイントでは、`timed_block` を使用してビジネスロジックを計測し、バリデーションエラーと成功イベントをログに記録します。

```python
# main.py (前のコードに追加)
from fastapi import Body
from typing import Annotated

from provide.foundation.errors import ValidationError
from provide.foundation.utils.timing import timed_block

# ... (前のコードはすべて上記と同じ)

@app.post("/users")
def create_user(username: Annotated[str, Body()])-> dict:
    """新しいユーザーを作成するエンドポイント。"""
    with timed_block(logger, "create_user_endpoint", initial_kvs={"username": username}) as ctx:
        # 1. 入力の検証
        if not username or len(username) < 3:
            # バリデーションエラーをログに記録
            logger.warning(
                "Invalid username provided",
                domain="validation",
                action="input",
                status="failure",
                username=username,
            )
            # このエラーはキャッチされ、400レスポンスを返す
            raise ValidationError("Username must be at least 3 characters long")

        # 2. データベース操作のシミュレーション
        ctx["db_operation"] = "insert"
        logger.info(
            "User created in database",
            **{
                "db.system": "postgres",
                "db.operation": "insert",
                "db.table": "users",
                "db.outcome": "success",
            },
        )

        return {"status": "user created", "username": username}

# FastAPIがValidationErrorを処理するための例外ハンドラ
from fastapi.responses import JSONResponse

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": exc.message},
    )
```

### ステップ5：アプリケーションの実行とログの確認

これで完全なアプリケーションができました。ターミナルで `uvicorn` を使用して実行します。

```bash
uvicorn main:app --reload
```

次に、`curl` やウェブブラウザを使用してAPIにリクエストを送信します。

**成功したリクエスト:**

```bash
curl -X POST -H "Content-Type: application/json" -d '"provide-user"' http://127.0.0.1:8000/users
```

コンソールのログは次のようになります。

```
[🐘][➕][✅] User created in database db.table=users
[▶️] create_user_endpoint completed username=provide-user db_operation=insert duration_seconds=0.0
[➡️][✅] HTTP request handled http.url=http://127.0.0.1:8000/users http.response_time_ms=2.5 client.address=127.0.0.1
```

**失敗したリクエスト（バリデーションエラー）:**

```bash
curl -X POST -H "Content-Type: application/json" -d '"a"' http://127.0.0.1:8000/users
```

コンソールのログは次のようになります。

```
[🛡️][➡️][❌] Invalid username provided username=a
[▶️] create_user_endpoint completed username=a duration_seconds=0.0
[➡️][⚠️CLIENT] HTTP request handled http.url=http://127.0.0.1:8000/users http.response_time_ms=1.5 client.address=127.0.0.1
```

### まとめ

おめでとうございます！このチュートリアルでは、以下のことを学びました。

*   FastAPIの起動時に `provide.foundation` を設定する方法。
*   ミドルウェアを使用してすべてのHTTPリクエストを自動的にログに記録する方法。
*   `timed_block` を使用して特定の操作のパフォーマンスを計測する方法。
*   ビジネスロジック（バリデーション、成功）に関連するセマンティックイベントをログに記録する方法。

これらのパターンは、あらゆるウェブアプリケーションで堅牢で観測可能なロギングをセットアップするための強力な基盤となります。
