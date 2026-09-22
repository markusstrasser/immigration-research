import { mount } from 'svelte'
import App from './App.svelte'
import './app.css'

const target = document.getElementById('app')
try {
  mount(App, { target })
} catch (e) {
  target.textContent = e.stack || String(e)
}
addEventListener('error', (e) => {
  target.textContent = (e.error && e.error.stack) || e.message
})
