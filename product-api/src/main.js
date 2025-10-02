const { createApp, ref, onMounted, computed } = Vue;

const app = createApp({
  setup() {
    const productos = ref([]);
    const categorias = ref([]);
    const marcas = ref([]);
    const unidades = ref([]);
    const searchTerm = ref('');

    // API 1: Categorías (Python - Puerto 3001)
    const fetchCategorias = async () => {
      try {
        const response = await fetch('http://localhost:3001/');
        const data = await response.json();
        categorias.value = data;
        console.log('Categorías cargadas:', data);
      } catch (error) {
        console.error('Error fetching categorías:', error);
      }
    };

    // API 2: Marcas (Node.js - Puerto 3002)
    const fetchMarcas = async () => {
      try {
        const response = await fetch('http://localhost:3002/');
        const data = await response.json();
        marcas.value = data;
        console.log('Marcas cargadas:', data);
      } catch (error) {
        console.error('Error fetching marcas:', error);
      }
    };

    // API 3: Unidades (PHP - Puerto 3003)
    const fetchUnidades = async () => {
      try {
        const response = await fetch('http://localhost:3003/');
        const data = await response.json();
        unidades.value = data;
        console.log('Unidades cargadas:', data);
      } catch (error) {
        console.error('Error fetching unidades:', error);
      }
    };

    // API 4: Productos (Java - Puerto 8080)
    const fetchProductos = async () => {
      try {
        const response = await fetch('https://8080-firebase-product-service-java-1759371536787.cluster-fsmcisrvfbb5cr5mvra3hr3qyg.cloudworkstations.dev/api/v1/products');
        const data = await response.json();
        productos.value = data;
        console.log('Productos cargados:', data);
      } catch (error) {
        console.error('Error fetching productos:', error);
      }
    };

    const filteredProductos = computed(() => {
      if (!searchTerm.value) {
        return productos.value;
      }
      return productos.value.filter(producto =>
        producto.nom_pro.toLowerCase().includes(searchTerm.value.toLowerCase())
      );
    });

    // Función para obtener el nombre de la categoría
    const getCategoriaNombre = (id_cat) => {
      const categoria = categorias.value.find(cat => cat.id_cat === id_cat);
      return categoria ? categoria.nom_cat : 'Sin categoría';
    };

    // Función para obtener el nombre de la marca
    const getMarcaNombre = (id_marca) => {
      const marca = marcas.value.find(mar => mar.id_marca === id_marca);
      return marca ? marca.nom_marca : 'Sin marca';
    };

    // Función para obtener el nombre de la unidad
    const getUnidadNombre = (id_uni) => {
      const unidad = unidades.value.find(uni => uni.id_uni === id_uni);
      return unidad ? unidad.nom_uni : 'Sin unidad';
    };

    onMounted(() => {
      fetchCategorias();
      fetchMarcas();
      fetchUnidades();
      fetchProductos();
    });

    return {
      productos,
      categorias,
      marcas,
      unidades,
      searchTerm,
      filteredProductos,
      getCategoriaNombre,
      getMarcaNombre,
      getUnidadNombre,
    };
  },
  template: `
    <div class="container">
      <h1>Sistema de Gestión de Productos</h1>

      <div class="search-section">
        <input
          type="text"
          v-model="searchTerm"
          placeholder="Buscar productos por nombre..."
          class="search-input"
        >
      </div>

      <div class="stats">
        <div class="stat-card">
          <h3>Productos</h3>
          <p class="stat-number">{{ productos.length }}</p>
        </div>
        <div class="stat-card">
          <h3>Categorías</h3>
          <p class="stat-number">{{ categorias.length }}</p>
        </div>
        <div class="stat-card">
          <h3>Marcas</h3>
          <p class="stat-number">{{ marcas.length }}</p>
        </div>
        <div class="stat-card">
          <h3>Unidades</h3>
          <p class="stat-number">{{ unidades.length }}</p>
        </div>
      </div>

      <h2>Lista de Productos</h2>
      <div class="products-grid" v-if="filteredProductos.length > 0">
        <div v-for="producto in filteredProductos" :key="producto.id_pro" class="product-card">
          <h3>{{ producto.nom_pro }}</h3>
          <div class="product-details">
            <p><strong>Precio:</strong> ${{ producto.pre_pro.toFixed(2) }}</p>
            <p><strong>Stock:</strong> {{ producto.stk_pro }}</p>
            <p><strong>Categoría:</strong> {{ getCategoriaNombre(producto.id_cat) }}</p>
            <p><strong>Marca:</strong> {{ getMarcaNombre(producto.id_marca) }}</p>
            <p><strong>Unidad:</strong> {{ getUnidadNombre(producto.id_uni) }}</p>
            <p><strong>Estado:</strong> <span :class="producto.estado === 'Y' ? 'active' : 'inactive'">
              {{ producto.estado === 'Y' ? 'Activo' : 'Inactivo' }}
            </span></p>
          </div>
        </div>
      </div>
      <p v-else class="no-products">No se encontraron productos</p>

      <div class="data-sections">
        <div class="data-section">
          <h2>Categorías Disponibles</h2>
          <ul class="data-list">
            <li v-for="categoria in categorias" :key="categoria.id_cat">
              {{ categoria.nom_cat }}
            </li>
          </ul>
        </div>

        <div class="data-section">
          <h2>Marcas Disponibles</h2>
          <ul class="data-list">
            <li v-for="marca in marcas" :key="marca.id_marca">
              {{ marca.nom_marca }}
            </li>
          </ul>
        </div>

        <div class="data-section">
          <h2>Unidades Disponibles</h2>
          <ul class="data-list">
            <li v-for="unidad in unidades" :key="unidad.id_uni">
              {{ unidad.nom_uni }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  `
});

app.mount('#app');
