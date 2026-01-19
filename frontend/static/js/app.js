let contract;
let accounts;
let web3;

async function init() {
    if (window.ethereum) {
        web3 = new Web3(window.ethereum);
        await window.ethereum.request({ method: "eth_requestAccounts" });
        accounts = await web3.eth.getAccounts();

        const contractABI = [
            {
                "anonymous": false,
                "inputs": [
                    { "indexed": false, "internalType": "string", "name": "certID", "type": "string" },
                    { "indexed": false, "internalType": "string", "name": "holderName", "type": "string" },
                    { "indexed": false, "internalType": "string", "name": "issuer", "type": "string" },
                    { "indexed": false, "internalType": "string", "name": "issueDate", "type": "string" }
                ],
                "name": "CertificateIssued",
                "type": "event"
            },
            {
                "constant": false,
                "inputs": [
                    { "internalType": "string", "name": "_certID", "type": "string" },
                    { "internalType": "string", "name": "_holderName", "type": "string" },
                    { "internalType": "string", "name": "_issuer", "type": "string" },
                    { "internalType": "string", "name": "_issueDate", "type": "string" }
                ],
                "name": "issueCertificate",
                "outputs": [],
                "payable": false,
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "constant": true,
                "inputs": [
                    { "internalType": "string", "name": "_certID", "type": "string" }
                ],
                "name": "getCertificate",
                "outputs": [
                    { "internalType": "string", "name": "", "type": "string" },
                    { "internalType": "string", "name": "", "type": "string" },
                    { "internalType": "string", "name": "", "type": "string" }
                ],
                "payable": false,
                "stateMutability": "view",
                "type": "function"
            }
        ];
        

        const contractAddress = "0x9b1f7F645351AF3631a656421eD2e40f2802E6c0";
        // 🔹 Replace with new contract address

        contract = new web3.eth.Contract(contractABI, contractAddress);
        console.log("✅ Contract Initialized:", contract);
    } else {
        alert("⚠️ Please install MetaMask to use this app.");
    }
}

document.getElementById("issue-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const certId = document.getElementById("certId").value;
    const name = document.getElementById("name").value;
    const institution = document.getElementById("institution").value;
    const date = document.getElementById("date").value;

    try {
        // 🔹 Step 1: Check if certificate already exists
        const existingCert = await contract.methods.getCertificate(certId).call();
        if (existingCert[0] !== "") {
            alert("❌ Certificate with this ID already exists!");
            return;
        }

        // 🔹 Step 2: Issue new certificate if ID is unique
        await contract.methods.issueCertificate(certId, name, institution, date)
            .send({ from: accounts[0] });

        alert("✅ Certificate Issued Successfully!");
    } catch (error) {
        console.error("❌ Error issuing certificate:", error);
        alert("⚠️ Failed to issue certificate. See console for details.");
    }
});

window.addEventListener("load", init);
