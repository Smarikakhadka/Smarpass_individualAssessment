const passwordInput = document.getElementById("password");

// CHECK PASSWORD
passwordInput.addEventListener("input", async () => {
    const password = passwordInput.value;

    if (!password) return;

    const res = await fetch("/check", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ password })
    });

    const data = await res.json();

    document.getElementById("strength-text").innerText =
        `Strength: ${data.strength} (${data.score_percentage}%)`;

    document.getElementById("crack-time").innerText =
        `Crack Time: ${data.crack_time}`;

    document.getElementById("ml-result").innerText =
        `AI: ${data.ml_prediction} (${data.ml_reason})`;

    document.getElementById("user-bar").style.width =
        data.score_percentage + "%";

    const fill = document.getElementById("strength-fill");
    fill.style.width = data.score_percentage + "%";

    fill.style.background =
        data.strength === "Weak" ? "red" :
        data.strength === "Medium" ? "orange" : "green";

    // Issues
    const feedback = document.getElementById("feedback");
    feedback.innerHTML = "";
    data.feedback.forEach(i => {
        const li = document.createElement("li");
        li.innerText = i;
        feedback.appendChild(li);
    });

    // Suggestions
    const suggestions = document.getElementById("suggestions");
    suggestions.innerHTML = "";
    data.suggestions.forEach(i => {
        const li = document.createElement("li");
        li.innerText = i;
        suggestions.appendChild(li);
    });
});

// TOGGLE PASSWORD
function togglePassword() {
    const input = document.getElementById("password");
    const icon = document.getElementById("toggleIcon");

    if (input.type === "password") {
        input.type = "text";
        icon.classList.replace("fa-eye-slash", "fa-eye");
    } else {
        input.type = "password";
        icon.classList.replace("fa-eye", "fa-eye-slash");
    }
}

// GENERATE PASSWORD
async function generatePassword() {
    const res = await fetch("/generate");
    const data = await res.json();

    document.getElementById("generated-password").innerText =
        "Generated: " + data.generated_password;

    document.getElementById("generated-bar").style.width =
        data.generated_score + "%";

    const userWidth = document.getElementById("user-bar").style.width;
    const userScore = parseInt(userWidth) || 0;

    let message = "";

    if (data.generated_score > userScore) {
        message = "Generated password is stronger";
    } else if (data.generated_score < userScore) {
        message = "Your password is stronger";
    } else {
        message = "Both passwords are similar";
    }

    document.getElementById("comparison-text").innerText = message;
}