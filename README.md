# AI-Piping-DE Assignment 
## Objectives
As a Data Engineer, you are tasked with helping the Data Scientist with segmenting prospects (or leads) by academic field and company type (persona based segmentation). Your objective is to provide the persona of a lead, given a lead id and expose some basic statistics. Person includes academic field and company type for now.
You are given the following information
- [db] Leads are stored in mongodb with the following representation. Accessing the database will be done in python using beanie library
```bash
class Lead(Document):
  id: str = Field(default_factory=lambda: uuid4().hex)
  status: int = 0
  first_name: Optional[str] = None
  last_name: Optional[str] = None
  email: Optional[str] = None
  photo_url: Optional[str] = None
```
- [api] An api endpoint get_linkedin_data(email:str) provides you with a json output given a prospect email address as input. Sometimes the data value is None.
- [csv] An incomplete csv table containing the mapping field_of_study -> academic_field - [field_of_study_exercise.csv]
- This file is to be populated with new (field_of_study, academic) tuple as we discover new field_of_study
- company type depends on the number of employees to make it simple
- Startup if < 50
- Mid Market if 50 < # employees < 1000
- Multi National Company if > 1000

## Instructions
You are given the instructions to build the pipeline using python 3.* with a package manager of your choice.

### Setup
● Initialise a new python project with a package manager of your choice. It would include : Beanie to access mongodb via python.For mongodb you can use either
-  A local deployment of mongodb if familiar with it (preferred), OR
- A local deployment using testcontainer, OR
- Use ```mongomock-motor``` to mock access to a “virtual” mongodb, OR Another solution

### Data
● [db]
○ Write the code
- to initialise access to mongodb using python
- to optimise the extraction of the relevant data from the db without pulling all the document details

● [csv]
○ Write the python code to:
- Read the csv data (handle missing values)
- Expose basic operations like read from csv, write to csv etc...
- Prepare a summary report on the data cleaning process (e.g., number of missing values removed, mapping ratio)

● [api]
○ Write the python code to:
- Mock the api endpoint get_linkedin_data(email:str) to return the json file provided
- Extract transform and load the relevant data

● [db]
○ Propose a solution to store the resulting persona in mongodb. For this exercise you may assume that the number of features to describe a persona will grow with time.
- Expose basic operations
- Get persona from lead id, update persona details
- Extract from the db the set of lead ids given a specific persona.

● []
○ You may want to keep a record of the json result from the above [api]. You are given the choice between aws s3 and mongodb GridFS. Explain your choice and implement in python the read / write

### Submission

- Push your code to a public GitHub repository.
- Include a README.md with clear instructions on how to run the application, test it, and
any other relevant information.

### Evaluation Criteria
We will evaluate based on the following criteria
- Functionality: Does the application work as described?
- Code Quality: Is the code organised, clean, and free of bugs?
- Data Structure
- Documentation: Are the setup and usage instructions clear?

### References

- Beanie Documentation
- MongoDB website
- https://github.com/mongomock/mongomock
