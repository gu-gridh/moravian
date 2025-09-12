import 'vite/modulepreload-polyfill';
import '../css/custom.css';
import '../css/gridh.css';
import '../css/mobile.css';
import '../css/ui_iiif.css';
import OpenSeadragon from 'openseadragon';



document.addEventListener('DOMContentLoaded', function () {
    OpenSeadragon({
        id: "openseadragon-viewer",
        homeFillsViewer: false,
                immediateRender: false,
                visibilityRatio: 0.8,
                minZoomImageRatio: 0.8,
                maxZoomPixelRatio: 1,
                homeFillsViewer: false,
                showZoomControl: true,
                showHomeControl: true,
                showFullPageControl: true,
                showNavigator: true,
                navigatorPosition: "TOP_RIGHT",
                navigatorAutoFade: true,
                preserveViewport: true,
                fullPageButton: "full-page",
                zoomInButton: "zoom-in",
                zoomOutButton: "zoom-out",
                nextButton: "next-button",
                previousButton: "prev-button",
                showRotationControl: true,
                rotateLeftButton: "rotate-left",
                rotateRightButton: "rotate-right",
                homeButton: "home",
                gestureSettingsTouch: {
                    pinchRotate: true
                },
        prefixUrl: "/static/assets/images/openseadragon/",
        tileSources: {
            type: 'image',
            url: window.imageUrl
        }
    });
});