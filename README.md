# pydantic_workshop

Code demonstrated during pydantic workshop

## Set up

### Create virtual environment venv

```bash
python -m venv venv
```

### Activate venv

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

Pydantic has a few dependencies:

pydantic-core: Core validation logic for pydantic written in rust.  
typing-extensions: Backport of the standard library typing module.  
annotated-types: Reusable constraint types to use with typing.Annotated

### Example of how to run code

```bash
python fields.py
```

## Course Content

1. Why pydantic

2. What pydantic's goal is and its basic usage of model  
   2a. Basic usage  
   2b. Data coercion  
   2c. Model_validate vs instantiation  
   2d. Nested models

3. Field  
   3a. Optional field  
   3b. Default value  
   3c. validate_default  
   3d. Alias  
   3e. Annotated  
   3f. Numeric constraints  
   3g. String constraints  
   3h. Decimal constraints  
   3i. Dataclass constraints

4. Config  
   4a. Basic usage  
   4b. Configuration in the BaseModel in Smarter 4c. Tariff Common  
   4d. alias_generator  
   4e. arbitrary_types_allowed  
   4f. extra  
   4g. frozen  
   4h. populate_by_name  
   4i. validate_assignment

5. Parsing
6. Validation
7. Serialisation
8. Json Schema
