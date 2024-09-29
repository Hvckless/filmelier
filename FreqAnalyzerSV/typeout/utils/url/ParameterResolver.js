class ParameterResolver {
    resolveParameter(urlContext) {
        let result = [];
        urlContext.split("&").forEach((param) => {
            let paramFragment = param.split("=");
            if (paramFragment.length != 2) {
                throw new Error("parameter is not constructed correctly.");
            }
            else {
                let _map = {};
                _map[paramFragment[0]] = paramFragment[1];
                result.push(_map);
            }
        });
        return result;
    }
}
export default ParameterResolver;
