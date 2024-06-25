export class SuperscriptError extends Error {
    constructor(msg) {
        super()
        this.message = msg
    }
    
    toString() {
        return this.message
    }
}