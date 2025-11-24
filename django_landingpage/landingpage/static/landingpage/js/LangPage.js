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

///////////////////////////////////////////////////////////////////////////////////////////
// start part of plans of upgrade
// ===== TROCA ENTRE MENSAL E ANUAL =====
const toggleContainer = document.querySelector(".toggle-container");
const btnMensal = document.getElementById("btnMensal");
const btnAnual = document.getElementById("btnAnual");
const price1 = document.getElementById("price1");
const price2 = document.getElementById("price2");
const price3 = document.getElementById("price3");

// Preços
const prices = {
  mensal: ["R$297/mês", "R$1297/mês", "R$597/mês"],
  anual: ["R$2.970/ano", "R$12.970/ano", "R$5.970/ano"],
};

// Função para animar troca de preço
function animatePriceChange(element, newPrice) {
  element.style.opacity = "0";
  setTimeout(() => {
    element.innerHTML = `${newPrice.split("/")[0]}<span>/${newPrice.split("/")[1]}</span>`;
    element.style.opacity = "1";
  }, 200);
}

// Clique em “Mensal”
btnMensal.addEventListener("click", () => {
  if (!btnMensal.classList.contains("active")) {
    btnMensal.classList.add("active");
    btnAnual.classList.remove("active");

    // Move o fundo (bolha) para a esquerda
    toggleContainer.classList.remove("active");

    animatePriceChange(price1, prices.mensal[0]);
    animatePriceChange(price2, prices.mensal[1]);
    animatePriceChange(price3, prices.mensal[2]);
  }
});

// Clique em “Anual”
btnAnual.addEventListener("click", () => {
  if (!btnAnual.classList.contains("active")) {
    btnAnual.classList.add("active");
    btnMensal.classList.remove("active");

    // Move o fundo (bolha) para a direita
    toggleContainer.classList.add("active");

    animatePriceChange(price1, prices.anual[0]);
    animatePriceChange(price2, prices.anual[1]);
    animatePriceChange(price3, prices.anual[2]);
  }
});

///////////////////////////////////////////////////////////////////////////////////////////
// EFEITO DE SCROLL SUAVE EM LINKS INTERNOS
///////////////////////////////////////////////////////////////////////////////////////////
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      window.scrollTo({
        top: target.offsetTop - 80,
        behavior: "smooth",
      });
    }
  });
});

///////////////////////////////////////////////////////////////////////////////////////////
// ANIMAÇÃO AO ROLAR (revela elementos)
///////////////////////////////////////////////////////////////////////////////////////////
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("show");
    }
  });
});

document.querySelectorAll("section, .checkpoint").forEach((el) => observer.observe(el));

///////////////////////////////////////////////////////////////////////////////////////////
// EFEITO HOVER SUAVE NOS PLANOS
///////////////////////////////////////////////////////////////////////////////////////////
const planos = document.querySelectorAll(".plano");
planos.forEach((plano) => {
  plano.addEventListener("mouseenter", () => {
    plano.style.transition = "0.4s ease";
    plano.style.boxShadow = "0 0 20px rgba(159, 44, 191, 0.4)";
  });
  plano.addEventListener("mouseleave", () => {
    plano.style.transform = "scale(1)";
    plano.style.boxShadow = "none";
  });
});
// end part of plans of upgrade
///////////////////////////////////////////////////////////////////////////////////////////
