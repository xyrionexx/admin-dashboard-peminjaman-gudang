<script lang="ts">
	interface Product {
		id: number;
		name: string;
		description: string;
		price: number;
		image: string;
	}

	const products: Product[] = [
		{
			id: 1,
			name: 'Sample Product',
			description: 'Product description goes here',
			price: 99.99,
			image: '/placeholder.svg?height=200&width=300'
		},
		{
			id: 2,
			name: 'Another Product',
			description: 'Another great product with amazing features',
			price: 149.99,
			image: '/placeholder.svg?height=200&width=300'
		},
		{
			id: 3,
			name: 'Premium Item',
			description: 'High-quality premium product for professionals',
			price: 299.99,
			image: '/placeholder.svg?height=200&width=300'
		}
	];

	function handleEdit(productId: number): void {
		console.log('[v0] Edit product:', productId);
	}

	function handleDelete(productId: number): void {
		console.log('[v0] Delete product:', productId);
	}

	function formatPrice(price: number): string {
		return `$${price.toFixed(2)}`;
	}
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<h1 class="text-3xl font-bold text-gray-900">Products</h1>
		<button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
			Add Product
		</button>
	</div>

	<!-- Product Grid -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
		{#each products as product}
			<div class="bg-white rounded-lg shadow-sm border overflow-hidden">
				<img
					src={product.image || '/placeholder.svg'}
					alt={product.name}
					class="w-full h-48 object-cover"
				/>
				<div class="p-4">
					<h3 class="text-lg font-semibold text-gray-900">{product.name}</h3>
					<p class="text-gray-600 text-sm mt-1">{product.description}</p>
					<div class="flex items-center justify-between mt-4">
						<span class="text-xl font-bold text-gray-900">{formatPrice(product.price)}</span>
						<div class="flex space-x-2">
							<button
								onclick={() => handleEdit(product.id)}
								class="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors"
								>Edit</button
							>
							<button
								onclick={() => handleDelete(product.id)}
								class="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors"
								>Delete</button
							>
						</div>
					</div>
				</div>
			</div>
		{/each}
	</div>
</div>
