class ClassToggler{
    toggle(element:HTMLElement, classname:string){

        if(element.classList.contains(classname)){
            element.classList.remove(classname);
        }else{
            element.classList.add(classname);
        }
    }
}

export default ClassToggler;