const passwordInput = document.getElementById("password");

passwordInput.addEventListener("input", async () => {
    const password = passwordInput.value;

    const response = await fetch("/check", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ password })
    });

    const data = await response.json();

    // Strength text
    document.getElementById("strength-text").innerText = data.strength;

    // Strength bar
    const fill = document.getElementById("strength-fill");
    fill.style.width = (data.score * 20) + "%";

    if (data.strength === "Weak") fill.style.background = "red";
    else if (data.strength === "Medium") fill.style.background = "orange";
    else fill.style.background = "green";

    // Feedback
    const feedbackList = document.getElementById("feedback");
    feedbackList.innerHTML = "";

    data.feedback.forEach(item => {
        const li = document.createElement("li");
        li.innerText = item;
        feedbackList.appendChild(li);
    });
});