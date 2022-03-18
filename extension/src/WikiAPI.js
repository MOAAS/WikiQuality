import axios from "axios";

const API_URL = "https://en.wikipedia.org/w/api.php";


export function callAPI(params) {
    return axios.get(API_URL, { 
        params: {
            formatversion: 2,
            format: "json",
            origin: "*", // https://stackoverflow.com/questions/23952045/wikipedia-api-cross-origin-requests
            ...params,
        }
    }).then(res => res.data);
}

export function getPageContent(title) {
    return callAPI({
        action: "parse",
        page: title,
        prop: "wikitext|text|displaytitle|sections|images|categories",
    });
}