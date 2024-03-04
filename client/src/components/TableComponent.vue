<template>
  <div class="table-container" >
    <DataTable v-if="products.length > 0" class="data-table" :value="products"
      paginator :rows="50" 
      paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
      currentPageReportTemplate="{first} to {last} of {totalRecords}"
      tableStyle="min-width: 50rem"
      scrollable scrollHeight="350px" size="small" removableSort
      showGridlines
     >
      <template #header>
        <div class="data-table-header" >
          <Button icon="pi pi-external-link" @click="downloadCSV" label="CSV" />
          <Button icon="pi pi-external-link" @click="downloadXLSX" label="XLSX" />
        </div>
      </template>
      <Column field="prod" header="Product Title" style="min-width: 100px" sortable></Column>
      <Column field="name" header="Store" style="min-width: 100px" sortable></Column>
      <Column field="location" header="Location" style="min-width: 150px" sortable></Column>
      <Column field="price" header="Price" style="min-width: 100px" sortable>
        <template #body="slotProps">
            <span>{{formatPrice(slotProps.data.price)}}</span>
        </template>
      </Column>
      <Column field="prodUrl" header="Link" style="width: 70px">
        <template #body="slotProps">
            <a class="link" :href="slotProps.data.prodUrl" target="_blank" >Link</a>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script setup>
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import * as XLSX from 'xlsx/xlsx.mjs';
import { useDataStore } from '@/stores/data'
import { storeToRefs } from 'pinia'
import { ref, watch } from 'vue';
import useUtils from '@/components/composables/useUtils'


const store = useDataStore()
const { products, query } = storeToRefs(store)
const {formatPrice} = useUtils()

const showBrand = ref(false)

function convertToCSV(arr) {
  const array = [Object.keys(arr[0])].concat(arr);

  return array.map(it => {
    return Object.values(it).toString();
  }).join('\n');
}

function downloadCSV() {
  const csvData = convertToCSV(products.value);
  const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.setAttribute('download', `${query.value.replaceAll(' ', "_")}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

const downloadXLSX = () => {
  // Create a worksheet
  const ws = XLSX.utils.json_to_sheet(products.value);
  const ERow = Object.keys(ws).filter(key => key.includes('E'))

  for (const idx in ERow) {
    const thisUrl = ws[ERow[idx]].v
    // ws[DRow[idx]].v = "Open Link"
    ws[ERow[idx]].l = {Target: thisUrl}
  }

  // Create a workbook
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');

  // Generate a binary string
  const binaryString = XLSX.write(wb, { bookType: 'xlsx', type: 'binary' });

  // Convert binary string to character codes
  const binaryArray = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    binaryArray[i] = binaryString.charCodeAt(i);
  }

  // Create a blob from the binary array
  const blob = new Blob([binaryArray], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

  // Create a download link and trigger the download
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${query.value.replaceAll(' ', "_")}.xlsx`;
  a.click();
  window.URL.revokeObjectURL(url);
}

watch(products, (prods) => {
  if(!showBrand.value) {
    const prodsWithBrand = prods.filter((prod) => {
      return prod.brand
    })
    if (prodsWithBrand.length > 0) showBrand.value = true
  }
})

</script>

<style lang="scss" scoped>
.table-container {
  @apply w-[90vw] lg:w-[50vw] xl:w-auto;
  .data-table {
    &-header {
      @apply flex gap-3;
    }
  
    
  
    .row-title {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }

}
</style>