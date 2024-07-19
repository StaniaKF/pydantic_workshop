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
   4b. Configuration in the BaseModel in Smarter Tariff Common  
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;alias_generator  
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;arbitrary_types_allowed  
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;extra  
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;frozen  
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;populate_by_name  
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;validate_assignment

5. Parsing  
   5a. Data coercion: lax mode  
   5b. strict mode

6. Validation
7. Serialisation
8. Json Schema
9. Dataclasses
