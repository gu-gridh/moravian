import 'vite/modulepreload-polyfill';
import '../css/custom.css';
import '../css/gridh.css';
import '../css/mobile.css';
import OpenSeadragon from 'openseadragon';

document.addEventListener('DOMContentLoaded', function () {
    OpenSeadragon({
        id: "openseadragon-viewer",
        prefixUrl: "/static/assets/images/openseadragon/",
        tileSources: {
            type: 'image',
            url: window.imageUrl
        }
    });
});