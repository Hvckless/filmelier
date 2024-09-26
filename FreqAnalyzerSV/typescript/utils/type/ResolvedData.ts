import MIMEType from "./MIMEType.js";

/**
 * Array[Buffer, MIMEType]
 */
interface ResolvedData extends Array<Buffer|MIMEType>{
    0: Buffer,
    1: MIMEType
}

export default ResolvedData;