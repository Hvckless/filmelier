class Singleton{
    private constructor(){

    }
    public static getInstance:Singleton = new Singleton();


    public helloworld(){
        console.log("THIS IS SINGLETON");
    }
}

export default Singleton;