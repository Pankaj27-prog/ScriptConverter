document.getElementById("convertBtn").addEventListener("click", async () => {

    const text = document.getElementById("inputText").value;

    const fromScript =
        document.getElementById("fromScript").value;

    const toScript =
        document.getElementById("toScript").value;

    const response = await fetch("/convert", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: text,
            from_script: fromScript,
            to_script: toScript
        })
    });

    const data = await response.json();

    if (data.success) {
        document.getElementById("outputText").value =
            data.result;
    } else {
        alert(data.error);
    }
});