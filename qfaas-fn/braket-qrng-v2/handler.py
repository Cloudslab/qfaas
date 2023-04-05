from braket.circuits import Circuit
from qfaas import Backend, RequestData, Utils

# Define sdk name
sdk = "braket"

# Pre-processing input data
def pre_process(input):
    data = RequestData(input, sdk)
    return data


# Generate Quantum Circuit
def generate_circuit(input):
    circuit = Circuit().h(range(input))
    return circuit


# Post-processing output data
def post_process(job):
    output = Utils.qrng_counts_post_process(job)
    return output


def handle(event, context):
    # 1. Pre-processing
    requestData = pre_process(event)

    # 2. Generate Braket Quantum Circuit
    qc = generate_circuit(requestData.input)

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
