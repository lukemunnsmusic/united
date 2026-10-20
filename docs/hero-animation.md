# UNITED Nights hero animation preview

PR #4 replaces the traced SVG preview with the original transparent handwriting frames. Production, Squarespace, DNS, Hub, forms and credentials are outside this change.

## Artwork and geometry

- `assets/united-wordmark-white.png` is Luke's supplied PNG, unchanged: 1000 × 200, white RGB with alpha, transparent background. Visible UNITED bounds: (1,4)–(999,196). Renamed from the supplied UNITED-LogoBlk.png to describe its actual white pixels.
- Original combined hero artwork: 1200 × 595 from the existing Squarespace hero. UNITED bounds: (1,1)–(1199,232); NIGHTS bounds: (231,245)–(1058,582).
- Both replacement layers occupy this same coordinate system. Transparent padding in the new UNITED PNG is accounted for, rather than clipping a combined logo. There is exactly one NIGHTS image.
- Original animation source: Luke's downloaded `UNITED_Nights_Web_Animation_Pack.zip`. The unused source WebM has been removed from the served assets; the earlier lossless encoding remains in Git history.
- All 115 source frames were decoded in Chrome at 30 fps, with alpha intact. The source frame crop (30,32)–(1246,531) maps to the original NIGHTS bounds. `nights-original.webp` is a 479,082-byte lossy animated WebP (previously 2,239,204 bytes), single-play, 3833 ms, with original timing, brush texture and transparency. It retains 1216×499 resolution and all decoded frame timings (109 encoded frames; repeated source frames are combined). RGB quality 85, alpha quality 20, method 4. Side-by-side mid/final comparisons at the rendered desktop size show no visible change; no resizing was used. This avoids relying on browser-specific WebM alpha decoding. No traced paths or synthetic handwriting.
- `nights-final.png` is the final decoded source frame and is used for no-JavaScript, reduced-motion and failed-animation fallback.
- Responsive placement follows the original 24-column grid (11px gaps, 1600px content cap, 0.0215 row scaling) and 8-column phone layout. Reference measured at https://unitednights.com on 20 Oct 2026. Subpixel differences from Squarespace's responsive image resampling can remain below one CSS pixel at the measured sizes.

## Playback

Arrival plays once, holds the completed lettering, and replays only after the logo has completely left view and returns during an upward scroll. Small movements in the visible hero do not restart it. Bytes are fetched once and fresh object URLs restart playback; replaced URLs are revoked. Reduced-motion changes immediately restore the final PNG. Failed image decoding restores the same PNG, without duplicate artwork.

The existing YouTube background is revealed only while its API reports actual playback. Blocked or unavailable playback leaves a clean black hero instead of rendering player error text behind the logo. The video ID is unchanged. The original Squarespace video container uses `filter: contrast(0.8)`; the preview applies the same 80% contrast to the video iframe only, lifting blacks and softening highlights while preserving the logo whites.

## Verification

Chrome and WebKit desktop/phone viewport checks cover arrival, completed frame, scroll-return replay, no restart on small scroll movements, reduced motion and no horizontal overflow. Viewports: 390×844, 768×1024, 1440×900, 1920×1080. WebKit is a Safari-engine test, not a physical iPhone test. The handwriting itself does not depend on third-party video playback.

`python3 build.py` regenerates the committed homepage; a repeat build must make no further changes. Inspect the PR diff to confirm forms and non-homepage generated pages are unchanged. Deployment verification and exact final SHA are recorded in the PR description and AI Team Change Log after publication.

## Rollback

Before merge: close PR #4 to discard this animation preview, or restore an earlier reviewed PR revision. The forms connection is already merged separately through PR #3; this animation PR remains unmerged. If separately approved and merged later, revert the resulting squash commit through another reviewed PR. No DNS or credential rollback is needed.
