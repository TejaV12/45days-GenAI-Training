/* Auto update year */
document.getElementById("year").textContent = new Date().getFullYear();

/* Dynamic title for SEO */
document.title = "Varun Teja | Web Developer Portfolio";

/* Smooth scrolling */
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", e => {
        e.preventDefault();
        document.querySelector(link.getAttribute("href"))
            .scrollIntoView({ behavior: "smooth" });
    });
});

/* Structured Data for Google */
const schema = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Varun Teja",
    "jobTitle": "Web Developer",
    "url": "https://github.com/TejaV12/45days-GenAI-Training",
    "sameAs": [
        "https://github.com/TejaV12"
    ]
};

const script = document.createElement("script");
script.type = "application/ld+json";
script.text = JSON.stringify(schema);
document.head.appendChild(script);
