class Singleton {
    constructor() {
    }
    helloworld() {
        console.log("THIS IS SINGLETON");
    }
}
Singleton.getInstance = new Singleton();
export default Singleton;
