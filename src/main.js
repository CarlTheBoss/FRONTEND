const { createApp, ref, onMounted, computed } = Vue;

const app = createApp({
  setup() {
    const productos = ref([]);
    const api2Data = ref([]);
    const api3Data = ref([]);
    const searchTerm = ref('');

    const fetchProductos = async () => {
      try {
        const response = await fetch('https://5000-firebase-frontendgit-1759369699879.cluster-thle3dudhffpwss7zs5hxaeu2o.cloudworkstations.dev/productos');
        const data = await response.json();
        productos.value = data;
      } catch (error) {
        console.error('Error fetching productos:', error);
      }
    };

    const fetchApi2Data = async () => {
      try {
        // Reemplaza 'URL_API_2' con la URL de tu segunda API
        const response = await fetch('URL_API_2');
        const data = await response.json();
        api2Data.value = data;
      } catch (error) {
        console.error('Error fetching API 2 data:', error);
      }
    };

    const fetchApi3Data = async () => {
      try {
        // Reemplaza 'URL_API_3' con la URL de tu tercera API
        const response = await fetch('URL_API_3');
        const data = await response.json();
        api3Data.value = data;
      } catch (error) {
        console.error('Error fetching API 3 data:', error);
      }
    };

    const filteredProductos = computed(() => {
      if (!searchTerm.value) {
        return productos.value;
      }
      return productos.value.filter(producto =>
        producto.nombre.toLowerCase().includes(searchTerm.value.toLowerCase())
      );
    });

    onMounted(() => {
      fetchProductos();
      // Descomenta las siguientes líneas cuando estés listo para usar las otras APIs
      // fetchApi2Data();
      // fetchApi3Data();
    });

    return {
      productos,
      api2Data,
      api3Data,
      searchTerm,
      filteredProductos,
    };
  },
  template: `
    <div>
      <h1>Productos</h1>
      <input type="text" v-model="searchTerm" placeholder="Buscar productos...">
      <ul>
        <li v-for="producto in filteredProductos" :key="producto.id">{{ producto.nombre }}</li>
      </ul>

      <!-- Agrega aquí la lógica para mostrar los datos de la API 2 -->
      <!-- <h1>API 2 Data</h1>
      <ul>
        <li v-for="item in api2Data" :key="item.id">{{ item.name }}</li>
      </ul> -->

      <!-- Agrega aquí la lógica para mostrar los datos de la API 3 -->
      <!-- <h1>API 3 Data</h1>
      <ul>
        <li v-for="item in api3Data" :key="item.id">{{ item.name }}</li>
      </ul> -->
    </div>
  `
});

app.mount('#app');
