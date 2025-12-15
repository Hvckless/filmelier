class ParameterResolver {
    resolveParameter(urlContext) {
        let result = {};
        urlContext.split("&").forEach((param) => {
            let paramFragment = param.split("=");
            if (paramFragment.length != 2) {
                throw new Error("parameter is not constructed correctly." + ` parameter : ${urlContext}`);
            }
            else {
                result[paramFragment[0]] = paramFragment[1];
            }
        });
        return result;
    }
}
export default ParameterResolver;
