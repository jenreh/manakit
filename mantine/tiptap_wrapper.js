import '@mantine/core/styles.css';
import '@mantine/tiptap/styles.css';

import { createElement, memo, useEffect } from 'react';
import { useEditor } from '@tiptap/react';
import {
  RichTextEditor as MantineRichTextEditor,
  Link
} from '@mantine/tiptap';
import StarterKit from '@tiptap/starter-kit';
import Highlight from '@tiptap/extension-highlight';
import TextAlign from '@tiptap/extension-text-align';
import Subscript from '@tiptap/extension-subscript';
import Superscript from '@tiptap/extension-superscript';
import { Color } from '@tiptap/extension-color';
import TextStyle from '@tiptap/extension-text-style';
import Placeholder from '@tiptap/extension-placeholder';

export const RichTextEditorWrapper = memo(function Wrapper({
  content = '',
  onUpdate,
  editable = true,
  placeholder = '',
  variant,
  withTypographyStyles,
  labels,
  ...otherProps
}) {
  const editor = useEditor({
    extensions: [
      StarterKit.configure({ link: false }),
      Link,
      Highlight,
      TextAlign.configure({ types: ['heading', 'paragraph'] }),
      Subscript,
      Superscript,
      TextStyle,
      Color,
      ...(placeholder ? [Placeholder.configure({ placeholder })] : []),
    ],
    content: content,
    editable: editable,
    onUpdate: ({ editor }) => {
      if (onUpdate) {
        onUpdate(editor.getHTML());
      }
    },
  });

  useEffect(() => {
    if (editor && content !== editor.getHTML()) {
      editor.commands.setContent(content);
    }
  }, [content, editor]);

  useEffect(() => {
    if (editor) {
      editor.setEditable(editable);
    }
  }, [editable, editor]);

  if (!editor) {
    return null;
  }

  return createElement(
    MantineRichTextEditor,
    {
      editor: editor,
      variant: variant,
      withTypographyStyles: withTypographyStyles,
      labels: labels,
      ...otherProps,
    },
    createElement(
      MantineRichTextEditor.Toolbar,
      { sticky: true, stickyOffset: '0px' },
      createElement(
        MantineRichTextEditor.ControlsGroup,
        null,
        createElement(MantineRichTextEditor.Bold, null),
        createElement(MantineRichTextEditor.Italic, null),
        createElement(MantineRichTextEditor.Underline, null),
        createElement(MantineRichTextEditor.Strikethrough, null),
        createElement(MantineRichTextEditor.ClearFormatting, null),
        createElement(MantineRichTextEditor.Code, null),
        createElement(MantineRichTextEditor.Highlight, null)
      ),
      createElement(
        MantineRichTextEditor.ControlsGroup,
        null,
        createElement(MantineRichTextEditor.H1, null),
        createElement(MantineRichTextEditor.H2, null),
        createElement(MantineRichTextEditor.H3, null),
        createElement(MantineRichTextEditor.H4, null)
      ),
      createElement(
        MantineRichTextEditor.ControlsGroup,
        null,
        createElement(MantineRichTextEditor.Blockquote, null),
        createElement(MantineRichTextEditor.Hr, null),
        createElement(MantineRichTextEditor.BulletList, null),
        createElement(MantineRichTextEditor.OrderedList, null),
        createElement(MantineRichTextEditor.Subscript, null),
        createElement(MantineRichTextEditor.Superscript, null)
      ),
      createElement(
        MantineRichTextEditor.ControlsGroup,
        null,
        createElement(MantineRichTextEditor.Link, null),
        createElement(MantineRichTextEditor.Unlink, null)
      ),
      createElement(
        MantineRichTextEditor.ControlsGroup,
        null,
        createElement(MantineRichTextEditor.AlignLeft, null),
        createElement(MantineRichTextEditor.AlignCenter, null),
        createElement(MantineRichTextEditor.AlignRight, null),
        createElement(MantineRichTextEditor.AlignJustify, null)
      ),
      createElement(
        MantineRichTextEditor.ControlsGroup,
        null,
        createElement(MantineRichTextEditor.Undo, null),
        createElement(MantineRichTextEditor.Redo, null)
      )
    ),
    createElement(MantineRichTextEditor.Content, null)
  );
});
