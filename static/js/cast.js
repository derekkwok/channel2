/** The valid states for casting a video. */
const CASTABLE_STATES = ['CONNECTED'];

/** Channel 2 javascript application. */
class Channel2 {
    constructor() {
        this.session = null;
        this.registerFileLinks();
    }

    initializeCastApi() {
        const applicationId = chrome.cast.media.DEFAULT_MEDIA_RECEIVER_APP_ID;
        this.getCastContext().setOptions({
            receiverApplicationId: applicationId,
            autoJoinPolicy: chrome.cast.AutoJoinPolicy.ORIGIN_SCOPED,
        });
    }

    /** Registers an anchor tag to be castable. */
    registerFileLinks() {
        const links = document.getElementsByClassName('tag-video-link');
        for (const link of links) {
            link.onclick = this.handleFileLinkClick.bind(this);
        }
    }

    /**
     * Handles a click event on a file link.
     * @param {Event} e The click event.
     */
    handleFileLinkClick(e) {
        if (!this.shouldCast()) {
            return;
        }
        e.preventDefault();
        const url = e.target.getAttribute('href');
        const title = e.target.getAttribute('title');
        const options = {credentials: 'include'};
        fetch(url, options).then((response) => {
            this.cast(response.url, title);
        });
    }

    /**
     * Casts a URL.
     * @param {string} url The video link URL (not the file URL).
     * @param {string} title The title of the video.
     */
    cast(url, title) {
        this.session = this.getCastContext().getCurrentSession();
        const mediaInfo = new chrome.cast.media.MediaInfo(url, 'video');
        mediaInfo.metadata = new chrome.cast.media.MovieMediaMetadata();
        mediaInfo.metadata.title = title;
        const request = new chrome.cast.media.LoadRequest(mediaInfo);
        this.session.loadMedia(request);
    }

    /** Gets the cast context. */
    getCastContext() {
        return cast.framework.CastContext.getInstance();
    }

    /**
     * Whether the current video should be casted.
     * @returns {*}
     */
    shouldCast() {
        return CASTABLE_STATES.includes(this.getCastContext().getCastState());
    }
}

window.channel2 = new Channel2();
window['__onGCastApiAvailable'] = (isAvailable) => {
    if (isAvailable) {
        window.channel2.initializeCastApi();
    }
};
