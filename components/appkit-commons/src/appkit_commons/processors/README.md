# Processor Utilities

This module provides common utilities for AI processor implementations to eliminate code duplication and ensure consistency across different processor types.

## Overview

The `appkit_commons.processors` module centralizes repeated patterns found across multiple AI processors (OpenAI, Perplexity, KnowledgeAI, Lorem Ipsum, etc.) into reusable utility functions.

## Key Utilities

### `convert_messages_to_openai_format(messages)`

Converts internal `Message` objects to OpenAI chat completion format.

**Features:**
- Maps internal `MessageType` to OpenAI roles (user, assistant, system)
- Merges consecutive messages with the same role (except system messages)
- Filters out unsupported message types
- Ensures proper alternation of user/assistant messages per OpenAI requirements

**Example:**
```python
from appkit_commons.processors import convert_messages_to_openai_format
from appkit_assistant.backend.models import Message, MessageType

messages = [
    Message(type=MessageType.SYSTEM, text="You are a helpful assistant"),
    Message(type=MessageType.HUMAN, text="Hello"),
    Message(type=MessageType.HUMAN, text="How are you?"),  # Merged with previous
]

formatted = convert_messages_to_openai_format(messages)
# Result: [
#     {"role": "system", "content": "You are a helpful assistant"},
#     {"role": "user", "content": "Hello\n\nHow are you?"}
# ]
```

### `create_text_chunk(text, source, model=None, streaming=False, **extra_metadata)`

Creates text chunks with consistent metadata structure.

**Features:**
- Unified chunk creation across all processors
- Standardized metadata fields
- Flexible extra metadata support

**Example:**
```python
from appkit_commons.processors import create_text_chunk

chunk = create_text_chunk(
    text="Hello world",
    source="openai",
    model="gpt-4",
    streaming=True,
    session_id="abc123"
)
# Creates Chunk with:
# - type: ChunkType.TEXT
# - text: "Hello world"
# - chunk_metadata: {
#     "source": "openai",
#     "model": "gpt-4",
#     "streaming": "true",
#     "session_id": "abc123"
# }
```

### `validate_model_support(model_id, supported_models, processor_name)`

Validates that a model is supported by the processor.

**Features:**
- Consistent error messages across all processors
- Automatic logging of validation failures
- Raises `ValueError` if model not found

**Example:**
```python
from appkit_commons.processors import validate_model_support

# In your processor's process() method:
validate_model_support(
    model_id="gpt-4",
    supported_models=self.models,
    processor_name="OpenAI Chat Completions"
)
# Raises ValueError with clear message if model not supported
```

## Usage Pattern

Typical processor refactoring using these utilities:

**Before (duplicated code):**
```python
class MyProcessor(Processor):
    async def process(self, messages, model_id, ...):
        # Duplicate validation
        if model_id not in self.models:
            logger.error("Model %s not supported", model_id)
            raise ValueError(f"Model {model_id} not supported")
        
        # Duplicate message conversion
        formatted = []
        for msg in messages:
            if msg.type == MessageType.HUMAN:
                formatted.append({"role": "user", "content": msg.text})
            # ... more conversion logic
        
        # Duplicate chunk creation
        yield Chunk(
            type=ChunkType.TEXT,
            text=content,
            chunk_metadata={
                "source": "my_processor",
                "streaming": str(True),
                "model": model_id,
            }
        )
```

**After (using utilities):**
```python
from appkit_commons.processors import (
    convert_messages_to_openai_format,
    create_text_chunk,
    validate_model_support,
)

class MyProcessor(Processor):
    async def process(self, messages, model_id, ...):
        validate_model_support(model_id, self.models, "My Processor")
        
        formatted = convert_messages_to_openai_format(messages)
        
        yield create_text_chunk(
            content,
            source="my_processor",
            model=model_id,
            streaming=True,
        )
```

## Benefits

1. **DRY Principle**: Eliminates code duplication across 4+ processors
2. **Consistency**: Ensures uniform behavior and metadata structure
3. **Maintainability**: Changes to common logic only need to be made once
4. **Type Safety**: Proper type hints maintained throughout
5. **Testability**: Common logic can be tested independently

## Processors Refactored

The following processors have been refactored to use these utilities:

- ✅ `OpenAIChatCompletionsProcessor`
- ✅ `KnowledgeAIProcessor`
- ✅ `KnowledgeAIOpenAIProcessor`
- ✅ `LoremIpsumProcessor`

## Design Notes

### Circular Dependency Prevention

The module uses runtime imports (`import` inside functions with `noqa: PLC0415`) to avoid circular dependencies between `appkit_commons` and `appkit_assistant`. This is acceptable here since:

1. The imports are for type information only
2. Functions are called at runtime, not module load time
3. It maintains clear separation of concerns between packages

### Future Enhancements

Potential future utilities to add:
- Common error handling patterns
- Retry logic for API calls
- Rate limiting utilities
- Streaming chunk aggregation
- Token counting utilities
