from qiskit import *
from qiskit.algorithms import Shor
from qfaas import Backend, RequestData, Utils

# Define sdk name
sdk = "qiskit"

# Pre-processing input data
def pre_process(input):
    data = RequestData(input, sdk)
    return data


# Generate Quantum Circuit
def generate_shor_circuit(input: int):
    shor = Shor()
    shor_qc = shor.construct_circuit(N=input, measurement=True)
    return shor_qc


# Post-processing output data
def post_process(job, requestData):
    output = Utils.qfaas_post_process(job, ptype="shor", requestData=requestData)
    return output


def handle(event, context):
    # 1. Pre-processing
    requestData = pre_process(event)
    # Jump to the post processing step if postProcessOnly is set to True
    if requestData.postProcessOnly:
        job = post_process(requestData, requestData)
    else:
        # 2. Generate Quantum Circuit
        qc = generate_shor_circuit(requestData.input)

        # 3. Verify and get Backend information
        backend = Backend(requestData, qc)

        # 4. Submit job and wait up to 1 min for job to complete.
        job = backend.submit_job(qc)
        # 5. Post-process
        if job.jobResult:
            job = post_process(job, requestData)
            
    # 6. Generate response data and return to user
    response = Utils.generate_response(job)
    return response

