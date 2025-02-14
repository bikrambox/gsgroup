// builder.config.(js|ts)

import { defineConfig } from '@vueform/builder'
import simple from '@vueform/builder/presets/simple'

// You might place this anywhere else in your project
import '@vueform/builder/index.css';

export default defineConfig({
  preset: simple,
}) 
 
