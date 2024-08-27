import HelloImp from './helloImp.js'

class Hello{
    constructor(){
        let newHello:HelloImp = new HelloImp();

        let kingHello:HelloImp = new HelloImp();

        console.log(newHello.kinggod);
        console.log(kingHello.kinghello);

    }
}

export default Hello;