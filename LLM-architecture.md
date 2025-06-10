# Description of architecture for handling LLM jobs


## Requirements:

- No job should be performed more than once, unnecessarily
- Adding a job should not depend on the state of the current job stack
- Data cannot be overwritten or deleted, even by accident

## Jobs:

- A job is an ordered pair `(p,c)` where p is the text prompt and c is the configuration.
- The configuration involves data like which LLM to use, what the temperature is, what the seed is, and other parameters that specifies the LLM's operation
- `p` and `c` are complex structured data:
- `p` consists of the base prompt, prepended text, appended text and description of dynamically generated data.
- `c` consists of a list of parameters and the command used to build the actual command to invoke the LLM, depending on the platform used (like the API key, HTTP request type, etc.)

Jobs are best described using formats like XML or JSON. Of these, JSON is language agnostic while being simple to parse in python, making it the ideal choice. A sample job would look like:

```
"configuration":{
	"LLM_name":<name>,
	"seed":<value>,
	"command":<link to command generation script>
	...
}
"prompt":
{
	// since the prompts may be large, with repetition, the best way is to store a link to the prompt generation script here
}
```

## Executing Jobs:

- Given `job.json`, an execution script "execute.py" reads the file path as an argument, builds the prompt, builds the command and runs it. 

- For locally run LLMs, [ollama in python](https://pypi.org/project/ollama-python/) is an effective front-end to manage the LLM. 

- For LLMs run on a server, the exact method depends on the LLM being used. The unified frontend (linked in the slack) can be used instead of custom generating HTTP requests for each separate AI app. This helps security concerns as well as ease of engineering. The feasibility of this depends on whether it supports an API suitable for automation.

## Storing data:

- The results are stored as `result of job`.
- `result of job` is a unicode string. It may not be human readable since AI tends to structure responses using markdown.
- Analysis of `result of job` requires a markdown parser to analyze automatically and a markdown renderer to analyze manually
- The ordered pair `(link to job, result of job)` is stored in `<EPOCH>_<job file name>.json`
- The use of `<EPOCH>` ensures that if the process is run twice, the file is not overwritten.

## Accessing data:

- Reading files is expensive in terms of time.
- The process of data access must therefore minimize unnecessary read operations.

- In general, one job file maps to any number (including 0) result files. 
- If incomplete jobs refer to a placeholder `null-result`, then the relation between `job` and `result` is a function that is surjective but not injective, which changes over time.

### Finding the result of a given job:

- Given `job.json`, the file paths that would store its execution contents is extracted by looking up all filenames that match `\d+_job.json` in the results folder. 
- This search does not require reading any of the files in the results folder, saving time.
- This also avoids having to read the contents of `job.json`, saving more time.

### Finding the generating job given a result:

- Given `<EPOCH>_<job file name>.json`, the filename of the generating job is extracted by splicing the filename.
- This does not require reading any of the contents of the result file.
- This also does not require reading any of the job files.

## Managing jobs:

- A system is set up with a daemon that constantly scans a job folder.
- Any time a job without a result is found, a subprocess is spawned with the command to execute the job. 
- The ordered pair `(job-name,pid)` is stored in a table in the daemon's memory. Any job with an entry already in the table does not result in a new subprocess.
- When a subprocess is complete (either due to success, timeout or failure), table entry is dropped.
- If the process is successful, the result is written into the results folder
- In other cases, the whole job is re-done.

This system has two properties:

- No subprocess runs for more than the individual timeout limit.
- As long as undone jobs exist, the daemon spawns more subprocesses.

The daemon is run on a machine which doesn't also run the LLMs locally. It is assumed that the subprocesses involve sending requests to a remote machine and waiting.

To add a job, one simply generates `job.json` and moves it into the job folder.


