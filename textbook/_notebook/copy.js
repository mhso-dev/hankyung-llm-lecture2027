document.addEventListener('DOMContentLoaded', () => {
  async function copy(text, notebook) {
    const status = notebook.querySelector('.copy-status');
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        const field = document.createElement('textarea');
        field.value = text;
        field.style.cssText = 'position:fixed;left:-9999px;top:0';
        document.body.appendChild(field);
        field.select();
        const success = document.execCommand('copy');
        field.remove();
        if (!success) throw new Error('copy unavailable');
      }
      status.textContent = '코드를 복사했습니다. Jupyter 코드 셀에 붙여 넣으세요.';
    } catch (_) {
      status.textContent = '자동 복사가 제한되어 있습니다. 코드 영역을 선택해 복사하세요.';
    }
  }
  document.querySelectorAll('.notebook').forEach(notebook => {
    notebook.querySelectorAll('.copy-cell').forEach(button => {
      button.addEventListener('click', () => copy(button.parentElement.querySelector('.nb-source').textContent, notebook));
    });
    notebook.querySelector('.copy-all')?.addEventListener('click', () => {
      const sections = [...document.querySelectorAll('.notebook')]
        .filter(section => section.dataset.notebook === notebook.dataset.notebook);
      const source = sections.flatMap(section => [...section.querySelectorAll('.nb-source')])
        .map(cell => cell.textContent).join('\n\n');
      copy(source, notebook);
    });
  });
});
