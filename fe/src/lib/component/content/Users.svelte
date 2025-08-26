<script lang="ts">
	interface User {
		id: number;
		name: string;
		email: string;
		status: 'Active' | 'Inactive';
		joinedDate: string;
		avatar: string;
	}

	type UserStatus = 'All Users' | 'Active' | 'Inactive';

	let searchQuery: string = $state('');
	let selectedStatus: UserStatus = $state('All Users');

	const users: User[] = [
		{
			id: 1,
			name: 'John Doe',
			email: 'john@example.com',
			status: 'Active',
			joinedDate: 'Jan 15, 2024',
			avatar: '/placeholder.svg?height=40&width=40'
		},
		{
			id: 2,
			name: 'Jane Smith',
			email: 'jane@example.com',
			status: 'Active',
			joinedDate: 'Jan 10, 2024',
			avatar: '/placeholder.svg?height=40&width=40'
		},
		{
			id: 3,
			name: 'Bob Johnson',
			email: 'bob@example.com',
			status: 'Inactive',
			joinedDate: 'Dec 28, 2023',
			avatar: '/placeholder.svg?height=40&width=40'
		}
	];

	function getStatusColor(status: User['status']): string {
		return status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800';
	}

	function handleEdit(userId: number): void {
		console.log('[v0] Edit user:', userId);
	}

	function handleDelete(userId: number): void {
		console.log('[v0] Delete user:', userId);
	}
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<h1 class="text-3xl font-bold text-gray-900">Users</h1>
		<button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
			Add User
		</button>
	</div>

	<!-- Search and Filter -->
	<div class="flex flex-col sm:flex-row gap-4">
		<div class="flex-1">
			<input
				type="text"
				bind:value={searchQuery}
				placeholder="Search users..."
				class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
			/>
		</div>
		<select bind:value={selectedStatus} class="px-4 py-2 border border-gray-300 rounded-lg">
			<option>All Users</option>
			<option>Active</option>
			<option>Inactive</option>
		</select>
	</div>

	<!-- Users Table -->
	<div class="bg-white rounded-lg shadow-sm border overflow-hidden">
		<table class="w-full">
			<thead class="bg-gray-50">
				<tr>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
						>User</th
					>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
						>Email</th
					>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
						>Status</th
					>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
						>Joined</th
					>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
						>Actions</th
					>
				</tr>
			</thead>
			<tbody class="bg-white divide-y divide-gray-200">
				{#each users as user}
					<tr>
						<td class="px-6 py-4 whitespace-nowrap">
							<div class="flex items-center">
								<img
									class="h-10 w-10 rounded-full"
									src={user.avatar || '/placeholder.svg'}
									alt="User"
								/>
								<div class="ml-4">
									<div class="text-sm font-medium text-gray-900">{user.name}</div>
								</div>
							</div>
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{user.email}</td>
						<td class="px-6 py-4 whitespace-nowrap">
							<span
								class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full {getStatusColor(
									user.status
								)}">{user.status}</span
							>
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{user.joinedDate}</td>
						<td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
							<button
								onclick={() => handleEdit(user.id)}
								class="text-blue-600 hover:text-blue-900 mr-3">Edit</button
							>
							<button onclick={() => handleDelete(user.id)} class="text-red-600 hover:text-red-900"
								>Delete</button
							>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
