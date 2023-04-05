import qsharp
from QSFaaS import GenerateRandomNumber
from qfaas import Backend, RequestData, Utils

# Define sdk name
sdk = "qsharp"

# Pre-processing input data
def pre_process(input):
    data = RequestData(input, sdk)
    return data


# Post-processing output data
def post_process(job):
    pass
    return job


def handle(event, context):
    # 1. Pre-processing
    requestData = pre_process(event)

    # 2. Generate Quantum Circuit
    qc = GenerateRandomNumber

    # 3. Verify and get Backend information
    backend = Backend(requestData, qc)

    # 4. Submit job and wait up to 1 min for job to complete.
    job = backend.submit_job(qc)

    # 5. Post-process
    if job.jobResult:
        job = post_process(job)
    response = Utils.generate_response(job)

    # 6. Send back the result
    return response
