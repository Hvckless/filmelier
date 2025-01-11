class URLRedirector {
    redirect(res, targetURL) {
        res.writeHead(302, {
            'Location': targetURL
        });
        res.end();
        return;
    }
}
export default URLRedirector;
