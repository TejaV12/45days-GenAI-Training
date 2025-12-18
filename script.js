/* Dynamic Page Title */
document.title = "Varun Teja | Web Developer Portfolio";

/* Dynamic Meta Description */
const metaDescription = document.querySelector('meta[name="description"]');
metaDescription.setAttribute(
    "content",
    "Varun Teja's personal portfolio showcasing skills in HTML, CSS, JavaScript, and GitHub."
);

/* Auto Update Copyright Year */
document.getElementById("year").textContent = new Date().getFullYear();

/* Smooth Scrolling (UX improvement) */
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
        e.preventDefault();
        document.querySelector(link.getAttribute('href'))
            .scrollIntoView({ behavior: 'smooth' });
    });
});

/* Structured Data for Google (JSON-LD) */
const structuredData = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Varun Teja",
    "jobTitle": "Web Developer",
    "url": "https://tejav12.github.io/3-2/",
    "sameAs": [
        "https://github.com/TejaV12"
    ]
};

const script = document.createElement("script");
script.type = "application/ld+json";
script.text = JSON.stringify(structuredData);
document.head.appendChild(script);
