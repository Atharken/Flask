

const themeButton = document.getElementById("theme-toggle");

// Restore the user's theme preference
const savedTheme = localStorage.getItem("finance-theme");

if (savedTheme === "dark") {
    document.body.classList.add("dark");
}

function updateThemeButton() {
    if (!themeButton) return;

    const isDark = document.body.classList.contains("dark");

    themeButton.textContent = isDark ? "☀️ Light mode" : "🌙 Dark mode";
    themeButton.setAttribute("aria-pressed", String(isDark));
    themeButton.setAttribute(
        "aria-label",
        isDark ? "Switch to light mode" : "Switch to dark mode"
    );
}

updateThemeButton();

if (themeButton) {
    themeButton.addEventListener("click", () => {
        document.body.classList.toggle("dark");

        const theme = document.body.classList.contains("dark")
            ? "dark"
            : "light";

        localStorage.setItem("finance-theme", theme);
        updateThemeButton();
    });
}
