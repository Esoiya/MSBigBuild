export class Quota {

    constructor (
        
        public used_percentage: number,

        public free_percentage: number,

        public used_megabytes: number,

        public rag: string
    ) { }

}