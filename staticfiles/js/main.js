// Navbar change color on scroll
window.addEventListener("scroll", function() {

    const navbar = document.querySelector(".navbar");

    if (window.scrollY > 50) {
        navbar.classList.add("navbar-scrolled");
    } else {
        navbar.classList.remove("navbar-scrolled");
    }

});


// Smooth scroll
document.querySelectorAll("a").forEach(anchor => {

    anchor.addEventListener("click", function(e) {

        if (this.hash !== "") {

            e.preventDefault();

            const hash = this.hash;

            document.querySelector(hash).scrollIntoView({
                behavior: "smooth"
            });

        }

    });

});