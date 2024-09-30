class TransitionHandler {
    applyTransition() {
        let module = document.querySelectorAll(".waitTransition");
        module.forEach((element) => {
            if (element.classList.contains("trans-Nav")) {
                element.classList.add("transition-navigation");
            }
            if (element.classList.contains("trans-WidthHeight")) {
                element.classList.add("transition-WidthHeight");
            }
        });
    }
}
export default TransitionHandler;
