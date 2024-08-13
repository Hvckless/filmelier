self.onmessage = (event)=>{
    postMessage(event.data[0] + event.data[1]);

    new TestWorker().helloworld();
}

class TestWorker{
    public helloworld(){
        postMessage("REALLY?");
    }
}