# Event Enrichment System

The Event Enrichment System in `provide.foundation` is a powerful feature that allows for the dynamic addition of visual markers, metadata, and transformations to log events based on their content. This system enhances the observability of applications by making logs more informative and easier to parse visually.

## Core Concepts

The system is built around three core components:

- **Event Mappings**: Define how to enrich log events based on the values of specific fields.
- **Field Mappings**: Associate log fields with event sets, enabling the application of enrichment rules.
- **Event Sets**: Collections of event and field mappings that define a complete enrichment domain.

## Configuration

The Event Enrichment System is configured through `EventSet` objects, which can be registered with the `EventSetRegistry`. The `EventSetResolver` then uses these configurations to enrich log events as they are processed.

## Usage

To use the Event Enrichment System, you need to:

1.  Define your `EventSet` configurations.
2.  Register your `EventSet` objects with the `EventSetRegistry`.
3.  Ensure that the `EventSetResolver` is included in your logger's processor chain.

Once configured, the system will automatically enrich log events that match the defined rules, adding visual markers, metadata, and applying transformations as specified.