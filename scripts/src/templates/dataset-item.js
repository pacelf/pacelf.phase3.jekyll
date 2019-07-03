export default (data) => (
`<dataset>
  <h3><a href="${data.url}">${data.title}</a></h3>
  <em>
  ${data.organization || ''}
  </em>
  </p>
  ${data.notes || ''}
</dataset>`
)
