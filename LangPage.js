class SampleNavbar{
    constructor(menusample, navList, NavLinks) {
        this.menusample = document.querySelector(menusample);
        this.navList = document.querySelector(navList);
        this.navLinks = document.querySelectorAll(NavLinks);
        this.activeClass = 'active';

        this.handleClick = this.handleClick.bind(this);
    }
    
    animeteLinks(){
        this.navLinks.forEach((link, index) => {
            link.style.animation
            ? (link.style.animation = '')
            : (link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`);

        });
    }

    handleClick(){
        this.navList.classList.toggle(this.activeClass);
        this.menusample.classList.toggle(this.activeClass);
        this.animeteLinks();
    }

    addClickEvent() {
        this.menusample.addEventListener("click", this.handleClick)
    }
    Init(){
        if(this.menusample) {
            this.addClickEvent();
        }
        return this;
    }
}

const sampleNavbar = new SampleNavbar(
    ".menu-sample",
    ".nav-list",
    ".nav-list li",
);
sampleNavbar.Init();