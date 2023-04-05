namespace QSFaaS {
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Diagnostics;

    operation GenerateRandomNumber(input : Int) : Int {
        mutable randomBits = [];
        mutable randomNumber = 0;
        use qubits = Qubit[input];
        for qubit in qubits {
            H(qubit);
            set randomBits += [M(qubit)];
            Reset(qubit);
        }
        set randomNumber = ResultArrayAsInt(randomBits);
        return randomNumber;
    }
}