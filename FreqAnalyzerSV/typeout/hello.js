import HelloImp from './helloImp.js';
class Hello {
    constructor() {
        let newHello = new HelloImp();
        let kingHello = new HelloImp();
        console.log(newHello.kinggod);
        console.log(kingHello.kinghello);
    }
}
export default Hello;
