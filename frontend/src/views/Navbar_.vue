<template>
  <Disclosure as="nav"
    class="bg-gray-200 dark:bg-gray-900 text-gray-900 dark:text-gray-400 sticky top-0 left-0 right-0 z-50"
    v-slot="{ open }">
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
      <div class="relative flex h-16 items-center justify-between">
        <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
          <!-- Mobile menu button-->
          <DisclosureButton
            class="relative inline-flex items-center justify-center rounded-md p-2 hover:bg-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-50 hover:text-white focus:outline-hidden focus:ring-inset">
            <span class="absolute -inset-0.5" />
            <span class="sr-only">Open main menu</span>
            <Bars3Icon v-if="!open" class="block size-6" aria-hidden="true" />
            <XMarkIcon v-else class="block size-6" aria-hidden="true" />
          </DisclosureButton>
        </div>

        <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
          <div class="flex shrink-0 items-center">
            <img class="h-8 w-auto" src="https://tailwindui.com/plus-assets/img/logos/mark.svg?color=indigo&shade=500"
              alt="BHS logistics" />
          </div>
          <div class="hidden sm:ml-6 sm:block">
            <div class="flex space-x-4">
              <template v-for="item in navigation" :key="item.name">
                <!-- Regular menu items -->
                <a v-if="!item.hasDropdown" :href="item.href"
                  :class="[item.current ? 'bg-gray-300 dark:bg-gray-700 text-gray-800 dark:text-white' : 'text-gray-900 dark:text-gray-50 hover:bg-gray-300 dark:hover:bg-gray-700 hover:text-blue dark:hover:text-gray-50', 'rounded-md px-3 py-2 text-sm font-medium']"
                  :aria-current="item.current ? 'page' : undefined">
                  {{ item.name }}
                </a>

                <!-- Dropdown menu items -->
                <Menu v-else as="div" class="relative inline-block text-left">
                  <MenuButton
                    class="inline-flex items-center rounded-md px-3 py-2 text-sm font-medium text-gray-900 dark:text-gray-50 hover:bg-gray-300 dark:hover:bg-gray-700">
                    {{ item.name }}
                    <ChevronDownIcon class="ml-2 -mr-1 h-5 w-5" aria-hidden="true" />
                  </MenuButton>
                  <transition enter-active-class="transition ease-out duration-100"
                    enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100"
                    leave-active-class="transition ease-in duration-75"
                    leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                    <MenuItems
                      class="absolute left-0 z-10 w-48 origin-top-right  bg-gray-200 dark:bg-gray-900 text-gray-700 dark:text-gray-50   focus:outline-hidden">
                      <div class="py-1">
                        <MenuItem v-for="subItem in item.subItems" :key="subItem.name" v-slot="{ active }">
                        <a :href="subItem.href"
                          :class="[active ? 'bg-gray-300 dark:bg-gray-700 text-gray-800 dark:text-white' : 'text-gray-900 dark:text-gray-50 hover:bg-gray-300  dark:hover:bg-gray-700', 'text-sm font-medium', 'block px-4 py-2 ']">
                          {{ subItem.name }}
                        </a>
                        </MenuItem>
                      </div>
                    </MenuItems>
                  </transition>
                </Menu>
              </template>
            </div>
          </div>
        </div>

        <!-- Bell icon -->
        <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
          <button type="button" class="relative rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white">
            <span class="absolute -inset-1.5" />
            <span class="sr-only">View notifications</span>
            <BellIcon class="size-6" aria-hidden="true" />
          </button>

          <!-- Profile dropdown -->
          <Menu as="div" class="relative ml-3">
            <div>
              <MenuButton class="relative flex rounded-full bg-gray-50 dark:bg-gray-800 text-sm">
                <span class="absolute -inset-1.5" />
                <span class="sr-only">Open user menu</span>
                <img class="size-8 rounded-full"
                  src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                  alt="" />
              </MenuButton>
            </div>
            <transition enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95">
              <MenuItems
                class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-50 py-1 ring-1 shadow-lg ring-black/5 focus:outline-hidden">
                <MenuItem v-slot="{ active }">
                <a href="#"
                  :class="[active ? 'hover:bg-gray-300 dark:hover:bg-gray-700 outline-hidden' : '', 'block px-4 py-2 text-sm']">
                  Your Profile
                </a>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                <a href="#"
                  :class="[active ? 'hover:bg-gray-300 dark:hover:bg-gray-700 outline-hidden' : '', 'block px-4 py-2 text-sm']">
                  Settings
                </a>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                <a href="#"
                  :class="[active ? 'hover:bg-gray-300 dark:hover:bg-gray-700 outline-hidden' : '', 'block px-4 py-2 text-sm']">
                  Sign out
                </a>
                </MenuItem>
              </MenuItems>
            </transition>
          </Menu>
        </div>
      </div>
    </div>








    <DisclosurePanel class="sm:hidden absolute top-16 inset-x-0 z-50 bg-gray-50 dark:bg-gray-800 shadow-md">
      <div class="space-y-1 px-2 pt-2 pb-3">
        <template v-for="item in navigation" :key="item.name">
          <!-- Regular menu items -->
          <DisclosureButton v-if="!item.hasDropdown" as="a" :href="item.href" :class="[
            item.current
              ? 'bg-gray-300 dark:bg-gray-700 text-gray-900 dark:text-white'
              : 'text-gray-900 dark:text-gray-50 hover:bg-gray-200 dark:hover:bg-gray-700',
            'block w-full text-left rounded-md px-3 py-2 text-base font-medium'
          ]" :aria-current="item.current ? 'page' : undefined">
            {{ item.name }}
          </DisclosureButton>

          <!-- Dropdown items for mobile -->
          <Disclosure v-else v-slot="{ open: dropdownOpen }">
            <div class="space-y-1">
              <DisclosureButton :class="[
                'flex w-full items-center justify-between rounded-md px-3 py-2 text-base font-medium',
                'text-gray-900 dark:text-gray-50 hover:bg-gray-200 dark:hover:bg-gray-700'
              ]">
                <span>{{ item.name }}</span>
                <ChevronDownIcon class="ml-2 h-5 w-5 transform transition-transform duration-200"
                  :class="{ 'rotate-180': dropdownOpen }" aria-hidden="true" />
              </DisclosureButton>

              <DisclosurePanel class="pl-4 space-y-1 ml-3">
                <DisclosureButton v-for="subItem in item.subItems" :key="subItem.name" as="a" :href="subItem.href"
                  class="block w-full text-left rounded-md px-3 py-2 text-base font-medium text-gray-900 dark:text-gray-50 hover:bg-gray-200 dark:hover:bg-gray-700">
                  {{ subItem.name }}
                </DisclosureButton>
              </DisclosurePanel>
            </div>
          </Disclosure>
        </template>
      </div>
    </DisclosurePanel>

















  </Disclosure>
</template>

<script setup>
import { Disclosure, DisclosureButton, DisclosurePanel, Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { Bars3Icon, BellIcon, XMarkIcon } from '@heroicons/vue/24/outline'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'
import { ref } from 'vue';



// const navigation = [
//   { name: 'Dashboard', href: '#', current: true },
//   { name: 'Team', href: '#', current: false },
//   {
//     name: 'Projects',
//     href: '#',
//     current: false,
//     hasDropdown: true,
//     subItems: [
//       { name: 'Nomeco', href: '#', current: false },
//       { name: 'Novonordis', href: '#', current: false }
//     ]
//   },
//   { name: 'Calendar', href: '#', current: false },
// ]





// const navigation = [
//   { name: 'Dashboard', href: '#', current: true },
//   { name: 'Team', href: '#', current: false },
//   { 
//     name: 'Projects',
//     href: '#',
//     current: false,
//     hasDropdown: true,
//     subItems: [
//       { name: 'Nomeco', href: '#' },
//       { name: 'Novonordis', href: '#' }
//     ]
//   },
//   { name: 'Calendar', href: '#', current: false },
// ]

const navigation = ref([
  { name: 'Dashboard', href: '#', current: true },
  { name: 'Team', href: '#', current: false },
  {
    name: 'Projects',
    href: '#',
    current: false,
    hasDropdown: true,
    subItems: [
      { name: 'Nomeco', href: '#' },
      { name: 'Novonordis', href: '#' }
    ]
  },
  // ... other items
  { name: 'Calendar', href: '#', current: false },
]);


</script>