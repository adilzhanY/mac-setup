#!/usr/bin/env bash
# Download the mgpro sound effect library (CC0 only) into ~/.local/share/mgpro/sfx/<pack>/.
# Every pack below was checked by hand: Kenney packs ship a License.txt that says
# "License (Creative Commons Zero, CC0)", and every OpenGameArt page lists CC0 as its only licence.
# Re-running is safe: a pack folder that already exists is skipped (delete it to fetch again).
# Usage: fetch_sfx.sh [library root]   then run sfx_catalog.py to rebuild the catalogue.
set -euo pipefail

ROOT="${1:-$HOME/.local/share/mgpro/sfx}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$ROOT"

# pack | source page | author | download URL(s), space separated
PACKS='
kenney-ui-audio|https://kenney.nl/assets/ui-audio|Kenney|https://kenney.nl/media/pages/assets/ui-audio/490d233f68-1677590494/kenney_ui-audio.zip
kenney-interface-sounds|https://kenney.nl/assets/interface-sounds|Kenney|https://kenney.nl/media/pages/assets/interface-sounds/fa43c1dd4d-1677589452/kenney_interface-sounds.zip
kenney-impact-sounds|https://kenney.nl/assets/impact-sounds|Kenney|https://kenney.nl/media/pages/assets/impact-sounds/87b4ddecda-1677589768/kenney_impact-sounds.zip
kenney-digital-audio|https://kenney.nl/assets/digital-audio|Kenney|https://kenney.nl/media/pages/assets/digital-audio/216eac4753-1677590265/kenney_digital-audio.zip
kenney-casino-audio|https://kenney.nl/assets/casino-audio|Kenney|https://kenney.nl/media/pages/assets/casino-audio/2472606a04-1721639069/kenney_casino-audio.zip
kenney-rpg-audio|https://kenney.nl/assets/rpg-audio|Kenney|https://kenney.nl/media/pages/assets/rpg-audio/8e99002d76-1677590336/kenney_rpg-audio.zip
kenney-sci-fi-sounds|https://kenney.nl/assets/sci-fi-sounds|Kenney|https://kenney.nl/media/pages/assets/sci-fi-sounds/6b296f9ecf-1677589334/kenney_sci-fi-sounds.zip
kenney-music-jingles|https://kenney.nl/assets/music-jingles|Kenney|https://kenney.nl/media/pages/assets/music-jingles/f37e530b9e-1677590399/kenney_music-jingles.zip
remotion-cc0|https://www.remotion.dev/docs/sfx (each file links its Freesound original)|whoosh.wav: Woosh by 1bob, freesound.org/s/831936; whip.wav: SWSH_Badminton Racquet_Recording_01_JW Audio by JW_Audio, freesound.org/s/838766; mouse-click.wav: Mouse Click Sound.mp3 by Pixeliota, freesound.org/s/678248; shutter-modern.wav: DSLR Shutter fast 006.wav by ristooooo1, freesound.org/s/539136; shutter-old.wav: Werra.wav by hmilleo, freesound.org/s/409093 (the other remotion.media sounds are memes or not CC0 and are left out)|https://remotion.media/whoosh.wav https://remotion.media/whip.wav https://remotion.media/mouse-click.wav https://remotion.media/shutter-modern.wav https://remotion.media/shutter-old.wav
oga-gui-lokif|https://opengameart.org/content/gui-sound-effects|lokif|https://opengameart.org/sites/default/files/GUI_Sound_Effects_by_Lokif.7z
oga-ui-haeldb|https://opengameart.org/content/ui-sounds-0|haeldb|https://opengameart.org/sites/default/files/ui_sounds.zip
oga-swishes|https://opengameart.org/content/swishes-sound-pack|artisticdude|https://opengameart.org/sites/default/files/swishes.zip
oga-air-whoosh|https://opengameart.org/content/air-whoosh|pyranostudios|https://opengameart.org/sites/default/files/whoosh2_0.wav
oga-click-clips|https://opengameart.org/content/87-clickety-clips|owlishmedia|https://opengameart.org/sites/default/files/Click_Clips.zip
oga-3-pops|https://opengameart.org/content/3-pop-sounds|wubitog|https://opengameart.org/sites/default/files/3pops.zip
oga-pop-effects|https://opengameart.org/content/pop-effect-sounds|trezegames|https://opengameart.org/sites/default/files/p_1.ogg https://opengameart.org/sites/default/files/p_2.ogg https://opengameart.org/sites/default/files/p_3.ogg https://opengameart.org/sites/default/files/p_4.ogg https://opengameart.org/sites/default/files/p_5.ogg
oga-slide-pop|https://opengameart.org/content/a-slide-pop-sound|ezduzziteh|https://opengameart.org/sites/default/files/slidepop_0.mp3
oga-clicks-switches|https://opengameart.org/content/10-clicks-and-switches|starninjas|https://opengameart.org/sites/default/files/10_clicks_and_switches.zip
oga-button-clicks|https://opengameart.org/content/16-button-clicks|qubodup|https://opengameart.org/sites/default/files/independent_nu_ljudbank-buttons_and_clicks.7z
oga-ui-feedback|https://opengameart.org/content/ui-sound-effects-button-clicks-user-feedback-notifications|robin-lamb|https://opengameart.org/sites/default/files/ui_wav.zip
oga-ui-sounds|https://opengameart.org/content/ui-sounds|stumpystrust|https://opengameart.org/sites/default/files/sounds_2.zip
oga-ui-assorted|https://opengameart.org/content/7-assorted-sound-effects-menu-level-up|joth|https://opengameart.org/sites/default/files/UISoundEffects.zip
oga-interaction|https://opengameart.org/content/atmospheric-interaction-sound-pack|qubodup|https://opengameart.org/sites/default/files/krank_sounds.7z
oga-time-hit-wind|https://opengameart.org/content/wind-hit-time-morph|qubodup|https://opengameart.org/sites/default/files/qubodup-timehitwind.zip
oga-bell-dings|https://opengameart.org/content/bell-dingschimes|pwl|https://opengameart.org/sites/default/files/bell_ding1.wav https://opengameart.org/sites/default/files/bell_ding2.wav https://opengameart.org/sites/default/files/bell_ding3.wav https://opengameart.org/sites/default/files/bell_ding4.wav
oga-metal-dings|https://opengameart.org/content/4-metal-dingsrings|starninjas|https://opengameart.org/sites/default/files/ding_-_starninjas.zip
oga-scifi-50|https://opengameart.org/content/50-cc0-sci-fi-sfx|rubberduck|https://opengameart.org/sites/default/files/sci-fi-sfx.zip
oga-retro-synth-50|https://opengameart.org/content/50-cc0-retro-synth-sfx|rubberduck|https://opengameart.org/sites/default/files/50-CC0-retro-synth-SFX.zip
oga-breaking-75|https://opengameart.org/content/75-cc0-breaking-falling-hit-sfx|rubberduck|https://opengameart.org/sites/default/files/sfx_breaking_and_falling.zip
oga-100-sfx|https://opengameart.org/content/100-cc0-sfx|rubberduck|https://opengameart.org/sites/default/files/100-CC0-SFX_0.zip
'

echo "$PACKS" | while IFS='|' read -r pack page author urls; do
  [ -z "$pack" ] && continue
  dest="$ROOT/$pack"
  if [ -d "$dest" ]; then echo "skip $pack (exists)"; continue; fi
  mkdir -p "$TMP/$pack"
  for u in $urls; do
    f="$TMP/$pack/$(basename "$u")"
    curl -sfL --retry 3 -o "$f" "$u"
    case "$f" in
      *.zip) unzip -qo "$f" -d "$TMP/$pack/x" ;;
      *.7z) 7z x -y -o"$TMP/$pack/x" "$f" >/dev/null ;;
      *) mkdir -p "$TMP/$pack/x" && cp "$f" "$TMP/$pack/x/" ;;
    esac
  done
  mv "$TMP/$pack/x" "$dest"
  # Junk that ships inside some archives: previews, shortcuts, OS metadata.
  chmod -R u+w "$dest"
  find "$dest" \( -name '*.url' -o -name 'desktop.ini' -o -name 'Preview.ogg' -o -name '3pops.ogg' -o -name 'MenuSFXPreview.mp3' -o -name '.DS_Store' -o -name '__MACOSX' \) -prune -exec rm -rf {} +
  if [ ! -f "$dest/License.txt" ]; then
    cat > "$dest/LICENSE.txt" <<EOF
$pack by $author
Source: $page
License: CC0 1.0 Universal (public domain dedication), the only licence listed on the source page.
https://creativecommons.org/publicdomain/zero/1.0/
No attribution required, commercial use allowed.
EOF
  fi
  echo "ok   $pack ($(find "$dest" -type f \( -iname '*.ogg' -o -iname '*.wav' -o -iname '*.mp3' -o -iname '*.flac' \) | wc -l) sounds)"
done
