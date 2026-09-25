import { mount } from 'svelte'
import Prototypes from './Prototypes.svelte'
import '../app.css'

const target = document.getElementById('app')
try {
  mount(Prototypes, { target })
} catch (e) {
  target.textContent = e.stack || String(e)
}
addEventListener('error', (e) => {
  target.textContent = (e.error && e.error.stack) || e.message
})
