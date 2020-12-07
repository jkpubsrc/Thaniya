class ThaniyaTag extends HTMLElement {
	constructor() {
		super();
		var shadow = this.attachShadow({mode: "open"});

		const wrapper = document.createElement("span");
		wrapper.classList.add("thaniya");

		// Add styling to the shadow DOM
		var styles = document.createElement("style");
		styles.textContent = ".thaniya {" +
			"font-family: Merienda;" +
			"font-weight: 100;" +
		"}" +
		".thaniya::after {" +
			'content: "Thaniya";' +
		"}";

		shadow.appendChild(styles);
		shadow.appendChild(wrapper);
	}
}

// Define the new custom element
customElements.define("x-thaniya", ThaniyaTag);





