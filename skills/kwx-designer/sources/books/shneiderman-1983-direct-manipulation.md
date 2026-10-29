# Shneiderman (1983), Direct Manipulation: A Step Beyond Programming Languages

- **Citation:** Ben Shneiderman, "Direct Manipulation: A Step Beyond Programming Languages", IEEE Computer 16(8), pp. 57-69, August 1983. DOI 10.1109/MC.1983.1654471.
- **Copy read:** course reading PDF hosted by the University of Cambridge Computer Laboratory (cl.cam.ac.uk/~pr10/iui/shneiderman83.pdf, IEEE Xplore licensed copy). Full text read via pdftotext.
- **Used in:** `editors/canvas-and-direct-manipulation.md`, `editors/editor-foundations.md`, `editors/panels-workspaces-onboarding.md`, `editors/history-and-nondestructive.md`.

## The idea

Systems that let users operate on visible objects feel "satisfying" and make "the computer transparent", so users concentrate on the task. Examples analysed: full-screen display editors versus line editors, VisiCalc, spatial data management, video games, CAD and computer-aided design systems.

## The four principles (verbatim list)

1. Continuous representation of the object of interest.
2. Physical actions (movement and selection by mouse, joystick, touch screen) or labeled button presses instead of complex syntax.
3. Rapid, incremental, reversible operations whose impact on the object of interest is immediately visible.
4. Layered or spiral approach to learning that permits usage with minimal knowledge. Novices become "expert at level 1" then expand.

## Claimed benefits

Novices learn basic functionality quickly; experts work extremely rapidly; intermittent users retain concepts; error messages are rarely needed; users see immediately whether actions further their goals; less anxiety because actions are easily reversible; users feel in control and can predict responses.

## Display editor details that became modern rules

- Display the document in its final form (WYSIWYG): format errors become "immediately apparent".
- Cursor motion by physical means instead of commands like "UP 6".
- Labeled buttons act as "a permanent menu selection display", so users need not memorize syntax.
- The one-line view of a line editor is "like seeing the world through a narrow cardboard tube".

## Problems he names (still relevant)

- Graphic representations do not automatically improve performance; content matters more than graphics. "The wrong information, or a cluttered presentation, can lead to greater confusion."
- Icons must be learned: "a graphic icon ... may require as much or more learning time as a word."
- Representations can mislead.
- Graphics take space: "a tabular textual display of 50 document names is far more appealing than only 10 document graphic icons".
- Mixing metaphors adds complexity; metaphors need testing because users may not share the designer's model.

## Syntactic/semantic model

Syntactic knowledge (which key does delete) is arbitrary, memorized by rote, volatile, and differs between systems. Semantic knowledge (the concept of deleting a line) is structured, stable and transferable. Direct manipulation lets users act in the semantic domain with little syntax, which lowers "problem-solving load and stress".

## Lessons for the skill

- Every frequent operation should be a visible physical action with live feedback; typed syntax is the precision path, not the only path.
- Offer list views next to icon grids.
- Label icons or make labels available.
- Undo is part of the definition of direct manipulation, not an extra.
