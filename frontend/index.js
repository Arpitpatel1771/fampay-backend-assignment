const state = {
    getApiConfig: {
        page: 0,
        size: 20,
        requestPending: false,
        filter: '',
        orderBy: 'date',
        orderDirection: 'desc',
        enablePagination: true
    },
    data: [],

    resetState() {
        this.getApiConfig.page = 0;
        this.getApiConfig.size = 20;
        this.getApiConfig.requestPending = false;
        this.getApiConfig.enablePagination = true;
        this.data = []
    }
}

function lg(){
    console.log(...arguments)
}

function populateVideos(arrayOfVideoData, rebuild = false){
    let htmlString = ``
    

    arrayOfVideoData.forEach(videoData => {
        const videoId = videoData.video_id
        const youtubeBaseUrl = 'https://youtube.com'
        const channelUrl = `${youtubeBaseUrl}/channel/${videoData.channel_id}`
        htmlString += `
            <div class="card">
                <a href="${youtubeBaseUrl}/watch?v=${videoId}" target="_blank" class="video-link">
                    <img
                        src="${videoData.thumbnail}"
                        alt="thumbnail"
                        class="thumbnail"
                    />
                </a>
                <div class="content">
                    <div class="channel-profile">
                        <a href="${channelUrl}" class="channel-logo" target="_blank"
                            ><div class="channel-logo">${videoData.channel_title[0].toUpperCase()}</div></a
                        >
                    </div>
                    <div class="video-info">
                        <div class="title">
                            ${videoData.title}
                        </div>
                        <div class="channel-title">
                            <a href="${channelUrl}" class="channel-title" target="_blank">${videoData.channel_title}</a>
                        </div>
                        <div class="published-at">${videoData.published_info}</div>
                    </div>
                </div>
            </div>
        `
    })

    if (rebuild) {
        document.getElementById('video-grid').innerHTML = htmlString
    }else{
        document.getElementById('video-grid').innerHTML += htmlString
    }
}

function generateUrl(url, queryParams){
    // generates a proper url from queryParams
    // forgive my code here _/\_
    let temp = true
    for (let key in queryParams){
        url += temp ? '?' : '&'
        temp = false
        url += `${key}=${queryParams[key]}`
    }
    return url
}

async function getVideoData(){
    let newPage = state.getApiConfig.page + 1
    if(state.getApiConfig.totalPages && newPage > state.getApiConfig.totalPages){
        return
    }

    let url = generateUrl('http://localhost:8000/api/Landingpage/list',{
        page: newPage,
        size: state.getApiConfig.size,
        filter: state.getApiConfig.filter,
        orderBy: state.getApiConfig.orderBy,
        orderDirection: state.getApiConfig.orderDirection
    })
    
    state.getApiConfig.requestPending = true

    let response = await fetch(url, {
        method: "GET",
        redirect: "follow"
    })

    response = await response.text()
    response = await JSON.parse(response)
    if(response.responseCode === 200){
        state.data = [...state.data, ...response.payload]
        state.getApiConfig.totalPages = response.totalPages
        state.getApiConfig.page = newPage
        lg(state)
        populateVideos(response.payload)
    }
    
    state.getApiConfig.requestPending = false
}

function changeGridSizeForResponsiveness(){
    let width = window.innerWidth

    // Max width of the card will be 320, 350 was used for some breathing room
    let numberOfColumns = Math.floor(width / 350)
    numberOfColumns = numberOfColumns < 1 ? 1 : numberOfColumns
    const grid = document.getElementById('video-grid')
    grid.style.gridTemplateColumns = `${'auto '.repeat(numberOfColumns).trim()}`
}

async function handleScroll(event){
    const scrollTop = event.target.scrollTop;
    const scrollHeight = event.target.scrollHeight;
    const clientHeight = event.target.clientHeight;

    let scrollPercent = scrollTop/(scrollHeight - clientHeight)*100;
    if(scrollPercent > 80 && !state.getApiConfig.requestPending && state.getApiConfig.enablePagination){
        getVideoData()
    }
}

function refresh(){
    state.resetState();
    getVideoData()
    populateVideos(state.data, true)
}

function changeFilter(){
    state.getApiConfig.filter = document.getElementById('filter').value
    refresh()
}

function changeSortBy(){
    state.getApiConfig.orderDirection = document.getElementById('sort').value
    refresh()
}

async function search(){
    const query = document.getElementById('searchbox').value

    if(query===''){
        refresh()
    }else{
        let url = generateUrl(`http://localhost:8000/api/Landingpage/search`,{
            query: query
        })

        let response = await fetch(url, {
            method: "GET",
            redirect: "follow"
        })
    
        response = await response.text()
        response = await JSON.parse(response)
        if(response.responseCode === 200){
            state.getApiConfig.enablePagination = false
            populateVideos(response.payload, true)
        }
    }

}

// Initial Request
getVideoData()

// Event Listeners
document.getElementById('video-grid').addEventListener('scroll', handleScroll)
document.getElementById('filter').addEventListener('change', changeFilter)
document.getElementById('sort').addEventListener('change', changeSortBy)
document.getElementById('search-button').addEventListener('click', search)

// Responsiveness
changeGridSizeForResponsiveness()
window.addEventListener('resize', changeGridSizeForResponsiveness)