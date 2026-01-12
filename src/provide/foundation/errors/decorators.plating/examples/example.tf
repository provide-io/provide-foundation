locals {
  example_result = format(
    # Function arguments here
  )
}

output "function_result" {
  description = "Result of format function"
  value       = local.example_result
}
